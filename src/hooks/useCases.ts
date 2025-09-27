import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { supabase } from '@/integrations/supabase/client';

export const useCases = (unitId: string | undefined) => {
  return useQuery({
    queryKey: ['cases', unitId],
    queryFn: async () => {
      if (!unitId) return [];
      
      const { data, error } = await supabase
        .from('cases')
        .select('*')
        .eq('unit_id', unitId)
        .order('created_at', { ascending: false });
      
      if (error) throw error;
      return data;
    },
    enabled: !!unitId,
  });
};

export const useCreateCase = () => {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: async (caseData: any) => {
      const { data, error } = await supabase
        .from('cases')
极       .insert(caseData)
        .select()
        .single();
      
      if (error) throw error;
      return data;
    },
    onSuccess: (_, variables) => {
      queryClient.invalidateQueries({ queryKey: ['cases', variables.unit_id] });
    },
  });
};

export const useCaseMinutas = (caseId: string | undefined) => {
  return useQuery({
    queryKey: ['minutas', caseId],
    queryFn: async () => {
      if (!caseId) return [];
      
      const { data, error } = await supabase
        .from('minutas')
        .select(`
          *,
          profiles(first_name, last_name)
        `)
        .eq('case_id', caseId)
        .order('created_at', { ascending: false });
      
      if (error) throw error;
      return data;
    },
    enabled: !!caseId,
  });
};